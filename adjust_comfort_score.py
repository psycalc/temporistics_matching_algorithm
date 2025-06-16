import argparse
import os


def main():
    parser = argparse.ArgumentParser(description="Update comfort score for a relationship type")
    parser.add_argument("typology", help="Typology name, e.g. Temporistics")
    parser.add_argument("relationship", help="Relationship type to modify")
    parser.add_argument("score", type=int, help="New comfort score")
    parser.add_argument(
        "--data-dir", help="Custom data directory containing *_comfort_scores.json", default=None
    )
    args = parser.parse_args()

    if args.data_dir:
        os.environ["DATA_DIR"] = args.data_dir

    # Import after setting DATA_DIR so statistics_utils picks up the path
    from app.statistics_utils import update_comfort_score

    update_comfort_score(args.typology, args.relationship, args.score)
    print(
        f"Updated {args.typology} relationship '{args.relationship}' to score {args.score}"
    )


if __name__ == "__main__":
    main()
