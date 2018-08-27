# Cartello
Create [kanban boards](https://en.wikipedia.org/wiki/Kanban_board) to track projects from flat markdown files.

## Setup
* Clone the repository and enter the folder
* install [mistune](https://github.com/lepture/mistune) from pip, it is a dependency required for parsing markdown
* create a board in the "boards" directory and run `python3 cartello.py`

## How to create boards

Boards are generated from a markdown file. The URL will be the name of the file while the html of the page is generated from the content of the file.
In particular:

* h1: there can be only one h1 header per project and it is the title of the board.
* h3: every header is a new card of the board.
* list: every entry of the list is an entry of the card. Title can be specified like this 'Title: '.
* code blocks: a tag can be added with two backticks (code blocks). The tags support the colors supported by [bulma](https://bulma.io/documentation/overview/colors/).

#### Example

```
Shopping List
===

### Should buy

* `warning|Vegs` Salad: must be organic, call farmers from red address book
* Squash
* Oranges
* Peppers
* Cake: ask Grandpa for the name of the last one
* `danger|nope` Beer, avoid krieks

### Bought

* `Cheap` Tomatoes: must be green
* `info|Project B` Milk: raw is better

```

# Demo

You can view a demo of the output of cartello here

http://francescomecca.eu/cartello/shopping_list.html
