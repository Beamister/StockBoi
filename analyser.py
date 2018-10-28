import nltk
import statistics
from textblob import TextBlob
import math

from nltk.corpus import wordnet

def sigmoid(x):
    return 1 / (1 + ((2 * math.e) ** (-(x -600) / 400)))

def rate_article_sentiment(article):
    first_text_snippet = ""
    first_snippet_score = 0
    second_text_snippet = ""
    second_snippet_score = 0
    third_text_snippet = ""
    third_snippet_score = 0
    word_count = len(article['text'].split())
    sentence_polarities = []
    sentence_subjectivities = []
    positional_modifier = 10
    total_sentences = 0
    paragraphs = article['text'].split('\n')
    for paragraph in paragraphs:
        sentences = paragraph.split('.')
        total_sentences += len(sentences)
        for sentence in sentences:
            blob = TextBlob(sentence)
            blob_polarity = blob.polarity
            blob_subjectivity = blob.subjectivity
            if blob_polarity > first_snippet_score:
                third_text_snippet = second_text_snippet
                third_snippet_score = second_snippet_score
                second_text_snippet = first_text_snippet
                second_snippet_score = first_snippet_score
                first_text_snippet = sentence
                first_snippet_score = blob_polarity
            elif blob_polarity > second_snippet_score:
                third_text_snippet = second_text_snippet
                third_snippet_score = second_snippet_score
                second_text_snippet = sentence
                second_snippet_score = blob_polarity
            elif blob_polarity > third_snippet_score:
                third_text_snippet = sentence
                third_snippet_score = blob_polarity
            for i in range(positional_modifier):
                sentence_polarities.append(blob_polarity)
            sentence_subjectivities.append(blob_subjectivity)
        if positional_modifier > 5:
            positional_modifier -= 1
    headline_blob = TextBlob(article['headline'])
    #remove 0 values from polarities
    sentence_polarities = [value for value in sentence_polarities if value != 0]
    print("Polarities: ", sentence_polarities)
    score = statistics.mean(sentence_polarities)
    score = statistics.mean([score, headline_blob.polarity]) * 10
    if score > 1:
        score = 1
    word_count_weighting = sigmoid(word_count)
    stdv_of_subjectivities = 1 - statistics.pstdev(sentence_subjectivities)
    mean_of_subjectivities = 1 - statistics.mean(sentence_subjectivities)
    certainty =  statistics.mean([stdv_of_subjectivities, mean_of_subjectivities, word_count_weighting])
    return {'headline' : article['headline'], 'text1' : first_text_snippet, 'text2' : second_text_snippet,
            'text3' : third_text_snippet, 'datetime' : article['datetime'], 'score' : score,
            'certainty' : certainty, 'absolute_score' : abs(score)}

def get_score(dict):
    return dict['absolute_score']

def analyse(data):
    stock_name = data['metadata']['name']
    article_count = data['metadata']['article_count']
    result = {'metadata' : data['metadata'], 'articles' : {}}
    result['articles'] = {}
    article_scores = []
    article_certainties = []
    analysis_results = {}
    for article_index in range(article_count):
        article_analysis = rate_article_sentiment(data[article_index])
        analysis_results[article_index] = article_analysis
        article_scores.append(article_analysis['score'])
        article_certainties.append(article_analysis['certainty'])
    sorted_indices = sorted(analysis_results.values(), key=get_score)
    for result_article_index in range(article_count):
        result['articles'][result] = analysis_results[sorted_indices[result_article_index]]
    result['articles'] = sorted(analysis_results)
    result['metadata']['overall_score'] = statistics.mean(article_scores)
    result['metadata']['overall_certainty'] = statistics.mean(article_scores)
    return result
