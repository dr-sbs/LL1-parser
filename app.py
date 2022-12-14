from flask import Flask, render_template, redirect, url_for, request

from left_recursion import left_recursion
from left_factoring import left_factor
from first_n_follow import get_first, get_follow, prepare_grammar
from parse_table_generator import generate_parse_table
from parsing_program import parse_input

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        grammar: str = request.form.get("grammar", "")
        input_string: str = request.form.get("input_string", "")
        if grammar.strip():
            left_recursion_free_grammar = left_recursion(grammar)
            left_factored_grammar = left_factor(left_recursion_free_grammar[:])
            _, _, c, non_terminals, terminals = prepare_grammar(
                left_factored_grammar)

            first = {}
            follow = {f"{non_terminals[0]}": {'$'}}

            for each_non_terminal in non_terminals:
                get_first(each_non_terminal, first,
                          c, terminals, non_terminals)

            get_follow(follow, c, terminals, non_terminals, first)
            get_follow(follow, c, terminals, non_terminals, first)

            parse_table, ambiguous = generate_parse_table(
                first, follow, terminals,
                non_terminals, left_factored_grammar, c)

            if input_string:
                parsing_results = parse_input(
                    input_string, parse_table, non_terminals)
            else:
                parsing_results = None

            return render_template("index.html",
                                   left_recursion_free_grammar=left_recursion_free_grammar,
                                   left_factored_grammar=left_factored_grammar,
                                   grammar_body=grammar.strip(),
                                   first=first,
                                   follow=follow,
                                   terminals=terminals,
                                   non_terminals=non_terminals,
                                   parse_table=parse_table,
                                   ambiguous=ambiguous,
                                   parsing_results=parsing_results,
                                   input_string=input_string)
        else:
            return redirect(url_for("index"))
    with open("rules.txt", "r") as file:
        grammar_body = file.read()
    return render_template("index.html", grammar_body=grammar_body, start=True)
