"""Example: Analyzing Reddit and X (Twitter) social data using WriteGenius."""

from writegenius.integrations.social_analyzer import (
    SocialPost,
    analyze_social_posts,
    parse_x_timeline,
)


def main():
    print("--- 1. Polish Social Discourse Analysis (Reddit r/Polska Mock Sample) ---")
    reddit_samples = [
        SocialPost(id="r1", platform="reddit", text="Świetny nowy projekt open source dla programistów w Polsce! Bardzo polecam.", author="user_a"),
        SocialPost(id="r2", platform="reddit", text="Nowe zasady podatkowe dla programistów i przedsiębiorców wchodzą w życie od przyszłego kwartału.", author="user_b"),
        SocialPost(id="r3", platform="reddit", text="Władze miasta ogłosiły przetarg na modernizację infrastruktury drogowej.", author="user_c"),
        SocialPost(id="r4", platform="reddit", text="Niestety wystąpił okropny problem techniczny i system zanotował poważną awarię.", author="user_d"),
    ]

    reddit_report = analyze_social_posts(reddit_samples, lang="pl")
    print(reddit_report.summary())

    print("\n--- 2. English Tech Discourse Analysis (X / Twitter API Timeline Sample) ---")
    mock_x_api_response = [
        {
            "id": "1890001",
            "text": "WriteGenius brings accurate, zero-dependency linguistic evaluation to European languages.",
            "author_id": "ai_dev",
            "public_metrics": {"like_count": 89},
        },
        {
            "id": "1890002",
            "text": "Traditional Anglo-centric readability formulas collapse on inflected languages. Read the empirical benchmark.",
            "author_id": "linguist_tech",
            "public_metrics": {"like_count": 45},
        },
        {
            "id": "1890003",
            "text": "Pure Python, zero bloat, instant cold start. Truly an excellent building block for NLP pipelines.",
            "author_id": "oss_contributor",
            "public_metrics": {"like_count": 120},
        },
    ]

    x_posts = parse_x_timeline(mock_x_api_response)
    x_report = analyze_social_posts(x_posts, lang="en")
    print(x_report.summary())


if __name__ == "__main__":
    main()
