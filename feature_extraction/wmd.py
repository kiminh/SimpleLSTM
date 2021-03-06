
from pyemd import emd
from gensim.models import KeyedVectors
from gensim.test.utils import get_tmpfile
from preprocessing.pre_process import TextNormalization

class wordMoverDistance:

	def __init__(self):

		# save model to access it faster
		try:
			temp_path = get_tmpfile('word2vec_model')
			self.word_vectors = KeyedVectors.load(temp_path, mmap='r') #read word2vec model
		except:
			self.word_vectors = KeyedVectors.load_word2vec_format('./data/word2vec/GoogleNews-vectors-negative300.bin.gz', binary=True)
			self.word_vectors.init_sims(replace=True) # normalizes the vectors in word2vec class
			temp_path = get_tmpfile('word2vec_model')
			self.word_vectors.save(temp_path)

		self.normalize_text = TextNormalization()
		

	def compute_wm_distance(self, claim, sentences):
		
		
		claim = self.normalize_text.remove_stopWords_punc(claim) #remove stopwords and punctuations
		sentences = [self.normalize_text.remove_stopWords_punc(sentence) for sentence in sentences]#remove stopwords and punctuations
		similarities = [self.word_vectors.wmdistance(claim, sentence) for sentence in sentences]

		# print ("similarities ", similarities)
		sorted_similarities_index = sorted(range(len(similarities)), 
								key=similarities.__getitem__)

		highest_similarity_score = similarities[sorted_similarities_index[0]]

		return (sentences[sorted_similarities_index[0]], round(highest_similarity_score, 2))


if __name__ == '__main__':

	print ("wmd startin ")
	wmd = wordMoverDistance()
	print ("word2vec loaded")
	claim = 'diego is a good guy'
	print (['diego is a guy','diego is cool', 'diego is a bad guy','diego loves Portugal','diego is a researcher','some unrealted sentence'])
	relevant_sentence, score = wmd.compute_wm_distance(claim,['diego is a guy','diego is cool', 'diego is a bad guy','diego loves Portugal','diego is a researcher','some unrealted sentence'])
	print ("claim ", claim)
	print ("relevant sentence ", relevant_sentence)
	print ("score ", score)