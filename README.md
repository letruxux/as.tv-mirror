# as.tv-mirror

**as.tv-mirror**, the alternative client for [AnimeSaturn](https://animesaturn.tv). 

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/letruxux/as.tv-mirror
    ```

2. Open the project directory:

    ```bash
    cd as.tv-mirror
    ```

3. Install the required packages:

    ```bash
    python -m pip install -r requirements.txt
    ```

## Running the Application

Navigate to the cloned directory and run the following command:

```bash
python main.py
```

## Paths

### /
Search for your favorite anime.

### /anime?url=***
Explore basic information and episodes of a specific anime.

## API

### /episode?url=***
Retrieve a link to watch a specific episode.

### /search?q=***
Search for an anime using a query.
(this is used to bypass CORS restrictions)

### /episodes?url=***
Get a list of episodes for a particular anime.

### /info?url=***
Retrieve basic information about an anime.