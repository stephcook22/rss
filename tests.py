import processor
import unittest
import feeds

class TestProcessor(unittest.TestCase):

    def setUp(self):
        self.tup1 = ('the', 'cat', 'sat')

    def test_isDistanceZeroOnSameString(self):
        d = processor.DTWDistance(self.tup1, self.tup1)
        result = d.start()
        self.assertEqual(result, 0.0)
    
    def test_euclideanDistanceSameArticleisZero(self):
        vector1 = ('cricket','is','a','game','played','by','fools','watched','others')
        vector1 = feeds.create_word_vector(vector1)
        result = processor.get_euclidean_dif(vector1, vector1)
        self.assertEqual(result, 0.0)
        
    def test_euclideanDistanceLengthNormalisation(self):
        vector1 = ('cricket','is','a','game','played','by','fools','watched','others')
        vector1 = feeds.create_word_vector(vector1)
          #test data same article, doubled length to test normalisation
        vector2 = ('cricket','is','a','game','played','by','fools','watched','others','cricket','is','a','game','played','by','fools','watched','others')
        vector2 = feeds.create_word_vector(vector2)
        result = processor.get_euclidean_dif(vector1, vector2)
        self.assertEqual(result, 0.0)
        
    def test_euclideanDistanceDifferentArticle(self):
        vector1 = ('cricket','is','a','game','played','by','fools','watched','others')
        vector1 = feeds.create_word_vector(vector1)
          #test data same article, doubled length to test normalisation
        vector2 = ('bing','bong','boop','billa','zac','time','test','shane','red')
        vector2 = feeds.create_word_vector(vector2)aquire
        result = processor.get_euclidean_dif(vector1, vector2)
        self.assertAlmostEqual(result, 1.0, 4 )
        
    def test_WordnetSimilarity(self):
        words=('cat','dog')
        result = processor.wordnetSimilarity(words)
        self.assertEqual(result, 0.2)
        
    def test_wordWeightIsTinyFora(self):
        a = ('a',1)
        cat = ('cat',1)
        result1 = processor.get_word_weight(a)
        result1 = processor.get_word_weight(cat)
        self.assertGreater(cat, a)
    
    def test_wordWeightReactionToUnknownWords(self):
        result = processor.get_word_weight(('Samsung',1))
        self.assertEqual(result, 1)
        
    #test data, completely different document.
    #vector2 = [('bing',1),('bong',1),('boop',1),('billa',1), ('zac',1),('time',1),('test',1),('shane',1),('red',1)]



suite = unittest.TestLoader().loadTestsFromTestCase(TestProcessor)
unittest.TextTestRunner(verbosity=2).run(suite)
