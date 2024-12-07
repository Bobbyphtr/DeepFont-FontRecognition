# DeepFont-FontRecognition Scripts
This are scripts to create and preprocess the synthetic datasets
The script to train dataset reside on train.ipynb

## Form Recognition App
Windows Form App can be found on Results folder with [Paper](https://github.com/Bobbyphtr/DeepFont-FontRecognition/blob/master/Results/Paper%20DeepFont%20-%20IJMLC.pdf).

To make it work, you have to change few things:
1. Define a proper `Python` path and `DeepFontApi.py` path [here](https://github.com/Bobbyphtr/DeepFont-FontRecognition/blob/3780ff236457d6b5ddd79c9eefd30081143a0418/Results/FontRecFormsApp/FontRecFormsApp/MainForm.cs#L267-L268).
2. Inside `DeepFontApi.py`, define the path of the CNN Model [here](https://github.com/Bobbyphtr/DeepFont-FontRecognition/blob/3780ff236457d6b5ddd79c9eefd30081143a0418/DeepFontAPI.py#L36-L37).
    -  The CNN model is available in the [Google drive](https://drive.google.com/file/d/1YjO_7zXedG237yoABbUbqrO0mrdBQATx/view?usp=drive_link). 
3. Inside `DeepFontApi.py` Define `test_data_path` to the [dataset matrix.](https://github.com/Bobbyphtr/DeepFont-FontRecognition/blob/3780ff236457d6b5ddd79c9eefd30081143a0418/matrix_dataset_test_50_RBKN).

# License
MIT License

Copyright (c) 2024 Bobbyphtr

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
