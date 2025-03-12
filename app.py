# app.py
from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from werkzeug.utils import secure_filename
import tempfile
from huffman import HuffmanCoding  # We'll import your existing code

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file:
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Create Huffman coding instance
        h = HuffmanCoding(filepath)
        
        # Compress the file
        compressed_file_path = h.compress()
        
        # Return the compressed file for download
        return send_file(compressed_file_path, as_attachment=True)

@app.route('/decompress', methods=['POST'])
def decompress():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file and file.filename.endswith('.bin'):
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Create a Huffman coding instance
        h = HuffmanCoding(filepath)
        
        # Decompress the file
        decompressed_file_path = h.decompress(filepath)
        
        # Return the decompressed file for download
        return send_file(decompressed_file_path, as_attachment=True)
    
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)