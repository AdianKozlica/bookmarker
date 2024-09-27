# CLI Bookmarker

A command-line tool to read and store bookmarks from a simple .txt file. Each line in the file should contain a path and a URL separated by '->'.

## Description

CLI Bookmarker is a tool that allows you to manage your bookmarks from the command line. It reads a .txt file containing paths and URLs, and stores them in a structured format.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/cli-bookmarker.git
    ```
2. Navigate to the project directory:
    ```sh
    cd cli-bookmarker
    ```
3. Install the required dependencies (if any):
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To use the CLI Bookmarker, run the following command:

```sh
python bookmarker.py -f /path/to/bookmarks.txt
```
Given a bookmarks.txt file with the following content

## Usage

```
"/home" -> "https://example.com"
"/home/docs" -> "https://docs.example.com"
```

Running the command:

```sh

python bookmarker.py -f bookmarks.txt

```

Will parse the file and store the bookmarks in a structured format.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the GNU General Public License v2.0. See the [LICENSE](LICENSE) file for details.