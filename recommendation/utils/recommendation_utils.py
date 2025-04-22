from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recommendation.models import HandicraftProduct, Order
from collections import defaultdict



def get_similar_products(product, top_n=5):
    all_others = HandicraftProduct.objects.exclude(id=product.id)

    if not all_others.exists():
        return []

    docs = [product.name + " " + product.description] + [
        p.name + " " + p.description for p in all_others
    ]

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(docs)
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    top_indices = cosine_sim.argsort()[-top_n:][::-1]

    # 🛠 Fix: cast index to int
    similar_products = [all_others[int(i)] for i in top_indices]

    return similar_products


# 🔹 2. Helper: Build User → Product Map
def get_user_product_map():
    user_product_map = defaultdict(set)
    orders = Order.objects.select_related('user', 'product').filter(status='CONFIRMED')
    for order in orders:
        user_product_map[order.user.id].add(order.product.id)
    return user_product_map 

def jaccard_similarity(set1, set2):
    union = set1 | set2
    return len(set1 & set2) / len(union) if union else 0

def get_collaborative_recommendations(current_user_id, top_n=10):
    user_to_products = get_user_product_map()
    current_user_products = user_to_products[current_user_id]
    recommendation_scores = defaultdict(float)

    for user_id, products in user_to_products.items():
        if user_id == current_user_id:
            continue

        similarity = jaccard_similarity(current_user_products, products)
        if similarity == 0:
            continue

        for product_id in products - current_user_products:
            recommendation_scores[product_id] += similarity

    sorted_recommendations = sorted(recommendation_scores.items(), key=lambda x: x[1], reverse=True)
    product_ids = [pid for pid, score in sorted_recommendations][:top_n]

    return HandicraftProduct.objects.filter(id__in=product_ids)