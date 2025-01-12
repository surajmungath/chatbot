def analyze_keywords(sentence):
    # Lists of keywords to check
    game_keywords = ['game', 'play', 'gaming', 'player', 'score', 'level', 'win', 'lose']
    music_keywords = ['music', 'song', 'sing', 'melody', 'rhythm', 'tune', 'lyrics', 'beat']
    story_keywords = ['story', 'tale', 'narrative', 'fiction', 'plot', 'character', 'novel', 'book', 'read']
    
    # Convert sentence to lowercase for case-insensitive matching
    sentence = sentence.lower()
    
    # Find matches
    found_game_words = [word for word in game_keywords if word in sentence]
    found_music_words = [word for word in music_keywords if word in sentence]
    found_story_words = [word for word in story_keywords if word in sentence]
    
    result = {
        'has_game_keywords': len(found_game_words) > 0,
        'has_music_keywords': len(found_music_words) > 0,
        'has_story_keywords': len(found_story_words) > 0,
        'game_words': found_game_words,
        'music_words': found_music_words,
        'story_words': found_story_words
    }
    
    return result
