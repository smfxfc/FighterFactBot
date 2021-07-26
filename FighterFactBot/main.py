#! python3
"""Monitor /r/ufc and /r/mma comments and execute bot when triggered."""


from utils.praw_funcs import stream_comments


def main():
    stream_comments()


if __name__ == "__main__":
    main()
