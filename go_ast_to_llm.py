import os
import json
import requests
from tree_sitter import Language, Parser

# Firstly we load the Go language grammar
GO_LANGUAGE = Language('build/my-languages.so', 'go')

#Time to parse da Go code to generate an AST
def parse_go_code(code):
    parser = Parser()
    parser.set_language(GO_LANGUAGE)
    tree = parser.parse(code.encode('utf8'))
    return tree

#Convert the AST to JSON
def ast_to_json(node, source_code):
    def node_to_dict(node):
        children = [node_to_dict(child) for child in node.children] if node.children else []
        start_byte = node.start_byte
        end_byte = node.end_byte
        return {
            'type': node.type,
            'start_byte': start_byte,
            'end_byte': end_byte,
            'text': source_code[start_byte:end_byte],
            'children': children
        }
    return node_to_dict(node.root_node)

#Feeding the formatted AST to the LLM using an API call
def send_ast_to_llm(ast_json, api_url, api_key):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.post(api_url, headers=headers, json=ast_json)
    return response.json()

## You can replace the go code by providing the using with open and redirecting to the go code provided by rishit to test it out for this. Meanwhile i just used a basic hello world code lol. 
if __name__ == "__main__":
    go_code = """
    package main

    import "fmt"

    func main() {
        fmt.Println("Hello, World!")
    }
    """
    tree = parse_go_code(go_code)
    ast_json = ast_to_json(tree, go_code)
    
    # Example API endpoint and key (replace with your actual LLM API details)
    api_url = "https://api.example.com/v1/ast"
    api_key = "your_api_key_here"
    
    response = send_ast_to_llm(ast_json, api_url, api_key)
    print(json.dumps(response, indent=2))

