import re
import pickle
import xml.sax
import subprocess

from collections import defaultdict, Counter


class WikiXmlHandler(xml.sax.handler.ContentHandler):
    """Parse through XML data using SAX"""
    def __init__(self, file_name, regex=['\[{2}(.*?)\]{2}']):
        
        xml.sax.handler.ContentHandler.__init__(self)
        self._buffer = None
        self._values = {}
        self._current_tag = None
        self._pages = []
        self._regex = regex
        self.file_name = file_name
        self.pages_batch = 0
        #self.link_anchors_list = defaultdict(list)
        self.compress_script = 'compressor.sh'

    def characters(self, content):
        """Characters between opening and closing tags"""
        
        if self._current_tag:
            self._buffer.append(content)

    def startElement(self, name, attrs):
        """Opening tag of element"""
        
        if name in ('title', 'ns', 'redirect', 'text', 'id'):
            self._current_tag = name
            self._buffer = []

    def endElement(self, name):
        """Closing tag of element"""
        
        if name == self._current_tag:
            # Assign tag value is not assigned previously
            try:
                tmp = self._values[name] 
            except KeyError:
                self._values[name] = ' '.join(self._buffer)

        if name == 'page':
            # Check for redirect
            try:
                tmp = self._values['redirect']
                self._values['redirect'] = '1'
            except KeyError:
                self._values['redirect'] = '0'
            # Process article
            self.article = self.process_article()

            if self.article[1] == str(0):
                self._pages.append(self.article)
                # Reset valus dictionary
                self._values = {}    
                
                # Save data
                id_article = self.article[0]
                name_space = self.article[1]
                id_redirect = self.article[2]
                title_article = self.article[3]
                if len(self.article[4]) < 1:
                    #print('NO LINKS', self.article[4], title_article)
                    #links, anchors = '', []
                    links = []
                else:
                    #links, anchors = zip(*self.article[4])
                    links = self.article[4]
                    #for l,a in zip(links, anchors):
                    #    self.link_anchors_list[l].append(a)
                        
                text_article = self.article[5]
                #if title_article.strip().replace(' ', '_') == 'Inference':
                #    print(links, id_article)

                
                # File titles
                self.save_data(self.file_name + '_id_title' + '.txt', 
                                id_article, title_article)
                # File adjacency lists
                self.save_data(self.file_name + '_adj_lists' + '.txt', 
                                id_article, links)
                # File redirects
                if id_redirect == str(1):
                    self.save_data(self.file_name + '_redirected_to' + '.txt', 
                                    id_article, links)
                # File ns = 0
                if name_space == str(0):
                    self.save_data(self.file_name + '_only_articles' + '.txt',
                                    id_article, '')
                # File text article
                self.save_data(self.file_name + '_len_text_articles' + '.txt', 
                                id_article, len(text_article)) 
            else:
                self._pages.append(self.article)
                # Reset valus dictionary
                self._values = {}    
                
    
    @staticmethod
    def save_data(save_to, item1, item2, schema='{}\t{}'):
        with open(save_to, 'a+') as f:
            f.write(schema.format(item1, item2) + '\n')
            
    def compress_file(self, to_save):
        
        val = subprocess.check_call("./" + \
                                self.compress_script + \
                                " {}".format(to_save),
                                shell=True)
            
    
    def process_article(self): # title, ns, redirect, text, wiki_id, regex
        """Process a wikipedia article looking for hyperlinks"""
        
        # Get all the hyperlinks in the page
        links = list(map(lambda x: x.split('|')[0].strip().replace(' ', '_').split('#')[0].strip(),
                            re.findall(self._regex[0], self._values['text'])))
        


        return (self._values['id'], 
                self._values['ns'], 
                self._values['redirect'], 
                self._values['title'].strip().replace(' ', '_'), 
                links, 
                self._values['text'])
    
    
def parse_dump(raw_data_path, processed_data_path):
    print('HELLO')
    handler = WikiXmlHandler(file_name=processed_data_path)
    print('FIRST ', raw_data_path, processed_data_path)

    # Parsing object
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)

    for i, line in enumerate(subprocess.Popen('bzcat',
        stdin=open(raw_data_path),
        stdout=subprocess.PIPE, shell=True).stdout):

        parser.feed(line)

    # Compress
    handler.compress_file(handler.file_name + '_id_title' + '.txt')
    handler.compress_file(handler.file_name + '_adj_lists' + '.txt')
    handler.compress_file(handler.file_name + '_redirected_to' + '.txt')
    handler.compress_file(handler.file_name + '_only_articles' + '.txt')
    handler.compress_file(handler.file_name + '_len_text_articles' + '.txt')

    # Save anchor index
    #for l,a in handler.link_anchors_list.items():
    #    handler.link_anchors_list[l] = list(Counter(a).items())

    #with open(handler.file_name + '_link_anchors' + '.p', 'wb') as f:
    #    pickle.dump(handler.link_anchors_list, f)