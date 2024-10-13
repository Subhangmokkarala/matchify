import random

def calculate_similarity(user1, user2):
    common_artists = set(user1['top_artists']) & set(user2['top_artists'])
    common_tracks = set(user1['top_tracks']) & set(user2['top_tracks'])

    similarity_score = (len(common_artists) * 2 + len(common_tracks)) / (len(user1['top_artists']) + len(user1['top_tracks']))
    return similarity_score

def match_user(current_user, db):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE spotify_id != %s", (current_user['id'],))
    other_users = cursor.fetchall()

    best_match = None
    best_score = -1

    for user in other_users:
        similarity = calculate_similarity(current_user, user)
        if similarity > best_score:
            best_score = similarity
            best_match = user

    return {
        'best_match': best_match,
        'similarity_score': best_score
    }
