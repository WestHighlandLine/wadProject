import random
import generate_users
import generate_groups
import generate_posts
import generate_comments

if __name__ == "__main__":
    random.seed(2024)
    generate_users.main()
    generate_groups.main()
    generate_posts.main()
    generate_comments.main()
