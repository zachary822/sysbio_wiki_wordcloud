import argparse

from sysbio_wiki_wordcloud import save_word_cloud


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--comment", help="use comments to draw word cloud", action='store_true')
    parser.add_argument("-o", "--output", help="Output file name.", type=str, default="wordcloud.png")
    parser.add_argument("-w", "--width", help="Output file width", type=int, default=1920)
    parser.add_argument("--height", help="Output file height", type=int, default=1080)

    args = parser.parse_args()

    save_word_cloud(args.output, args.width, args.height, comment=args.comment)


if __name__ == "__main__":
    main()
