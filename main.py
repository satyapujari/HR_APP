"""Main CLI entry point for RAG application."""
import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv

from rag.rag_pipeline import RAGPipeline

def index_command(args):
    """Handle index command."""
    try:
        pipeline = RAGPipeline(args.config)
        pipeline.index_documents(args.path)
        print("\n✓ Documents indexed successfully!")
    except Exception as e:
        print(f"\n✗ Error indexing documents: {e}", file=sys.stderr)
        sys.exit(1)


def query_command(args):
    """Handle query command."""
    try:
        pipeline = RAGPipeline(args.config)

        # Load existing vector store
        pipeline.load_vectorstore()

        if args.interactive:
            # Interactive mode
            print("\n=== RAG Interactive Query Mode ===")
            print("Type 'exit' or 'quit' to exit\n")

            while True:
                try:
                    question = input("Question: ").strip()

                    if question.lower() in ['exit', 'quit']:
                        print("\nGoodbye!")
                        break

                    if not question:
                        continue

                    print("\nSearching and generating answer...\n")
                    result = pipeline.query(question)

                    print(f"Answer: {result['answer']}\n")

                    if args.show_sources:
                        print("Sources:")
                        for i, doc in enumerate(result['source_documents'], 1):
                            source = doc.metadata.get('source', 'Unknown')
                            page = doc.metadata.get('page', 'N/A')
                            print(f"  [{i}] {source} (Page {page})")
                        print()

                except KeyboardInterrupt:
                    print("\n\nGoodbye!")
                    break
                except Exception as e:
                    print(f"\n✗ Error: {e}\n", file=sys.stderr)
        else:
            # Single query mode
            if not args.question:
                print("Error: --question is required in non-interactive mode", file=sys.stderr)
                sys.exit(1)

            result = pipeline.query(args.question)

            print(f"\nQuestion: {result['question']}")
            print(f"\nAnswer: {result['answer']}\n")

            if args.show_sources:
                print("Sources:")
                for i, doc in enumerate(result['source_documents'], 1):
                    source = doc.metadata.get('source', 'Unknown')
                    page = doc.metadata.get('page', 'N/A')
                    print(f"  [{i}] {source} (Page {page})")

    except Exception as e:
        print(f"\n✗ Error during query: {e}", file=sys.stderr)
        sys.exit(1)

def main_noargs():
    # Load environment variables
    load_dotenv()

def main():
    """Main CLI entry point."""
    # Load environment variables
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="RAG Application - Index and query documents using Retrieval Augmented Generation"
    )

    parser.add_argument(
        '--config',
        type=str,
        default='config/config.yaml',
        help='Path to configuration file (default: config/config.yaml)'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Index command
    index_parser = subparsers.add_parser('index', help='Index documents')
    index_parser.add_argument(
        'path',
        type=str,
        help='Path to PDF file or directory containing PDFs'
    )

    # Query command
    query_parser = subparsers.add_parser('query', help='Query indexed documents')
    query_parser.add_argument(
        '-q', '--question',
        type=str,
        help='Question to ask (required in non-interactive mode)'
    )
    query_parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    query_parser.add_argument(
        '-s', '--show-sources',
        action='store_true',
        help='Show source documents'
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == 'index':
        index_command(args)
    elif args.command == 'query':
        query_command(args)


if __name__ == '__main__':
    main()