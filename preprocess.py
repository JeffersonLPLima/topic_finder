import re
import unidecode
from tqdm import tqdm

my_stopword_list = {'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'd', 'did', 'do', 'does', 'doing', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is', 'it', "it's", 'its', 'itself', 'just', 'll', 'm', 'ma', 'me', 'more', 'most', 'my', 'myself', 'no', 'now', 'o', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 're', 's', 'same', 'she', "she's", 'should', "should've", 'so', 'some', 'such', 't', 'than', 'that', "that'll", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 've', 'very', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'y', 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves'}
my_emoji_stopword = {'🏻','🏼','🏽','🏾','🏿','♂','♀'}
class Preprocess():
    def __init__(self):
        self.REGEX_REMOVE_PUNCTUATION = re.compile('[%s]' % re.escape('!¡"$%&\'()*+,.ªº/:;<=>#¿?[\\]^_`{|}~'))
        self.URL_RE = re.compile(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*')
        self.WWW_RE = re.compile(r'www?[-_.?&~;+=/#0-9A-Za-z]{1,2076}')
        self.MENTION_RE = re.compile(r'@[-_.?&~;+=/#0-9A-Za-z]{1,2076}')
        self.MAIL_RE = re.compile(r'\S*@\S*\s?')
        self.DIGIT_RE = re.compile(r"\S*\d\S*") #remove if contains digit
        self.REPEATED_LETTER =  re.compile(r"([a-q?=t-z])\1{1,}")
        self.LETTER_HIFEN = re.compile(r"(?<!\w)\W+|\W+(?!\w)") #remove hifen if hifen is between and len(1) guarda-roupa (keep) meu--deus (remove)
        


    def transform(self, texts):

        new_texts = []
        for t in tqdm(range(len(texts)), total=len(texts), position=0):
            sentence = texts[t].lower().replace("\n", "").replace("\t", " ").strip() 
            sentence = unidecode.unidecode(sentence)
            sentence =  self.MAIL_RE.sub(" ", sentence)
            sentence =  self.URL_RE.sub(" ", sentence)
            sentence =  self.WWW_RE.sub(" ", sentence)

            sentence =  self.REPEATED_LETTER.sub(r"\1", sentence)
            sentence =  self.MENTION_RE.sub(" ", sentence)
            sentence = self.LETTER_HIFEN.sub(" ", sentence)

            sentence =  self.REGEX_REMOVE_PUNCTUATION.sub(" ", sentence)
            sentence =  self.DIGIT_RE.sub("", sentence)

            new_texts.append([x for x in sentence.split() if x not in my_stopword_list])

        return new_texts
      