# Artificial Intelligence Tasks
This repo contains programs i did for the codsoft internship where i completed Ai related tasks, it was much fun to learn and build it. 


# Tic-Tac-Toe AI 
This is a Python implementation of the classic Tic Tac Toe game with an AI opponent using the minimax algorithm. The game is built using PyQt5 for the user interface.
The game follows the standard rules of Tic Tac Toe:
Players take turns to place their symbol (X for human player, O for AI) on a 3x3 grid.
The player who succeeds in placing three of their marks in a horizontal, vertical, or diagonal row wins the game.
If all cells are filled and no player has achieved a winning combination, the game ends in a draw.
The AI opponent uses the minimax algorithm to determine the best move it can make given the current board state. The algorithm explores all possible future moves recursively, assigning a score to each possible outcome. The AI aims to maximize its score while assuming the human player will also make optimal moves.

Packages required : `PyQt5` 

# Image Captioning AI
Python implementation of Image Captioning using BLIP model from Hugging Face's Transformers library

BLIP effectively utilizes the noisy web data by bootstrapping the captions, where a captioner generates synthetic captions and a filter removes the noisy ones
It is built with Gradio for user interface and provides super fast performance by utilizing Nvidia CUDA
- [Click here to download Pre-Trained Model](https://huggingface.co/Salesforce/blip-image-captioning-large)

Enter directory of where the model and processor is present in the code and run the python file
local host link will be in console which gives a website with simple interface to use the program.  

Packages required : `Gradio` `transformers` `pillow` 
