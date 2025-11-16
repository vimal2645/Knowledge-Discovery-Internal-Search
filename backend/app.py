from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from config import Config
from indexer import index_document, search_documents, get_all_categories

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload and indexing"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed. Use: txt, pdf, docx'}), 400
    
    try:
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Index the document
        success, message = index_document(filepath, filename)
        
        if success:
            return jsonify({
                'message': 'File uploaded and indexed successfully',
                'filename': filename
            }), 200
        else:
            return jsonify({'error': message}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search():
    """Search documents"""
    query = request.args.get('q', '')
    category = request.args.get('category', 'All')
    limit = int(request.args.get('limit', 20))
    
    if not query:
        return jsonify({'results': [], 'message': 'No query provided'}), 200
    
    results = search_documents(query, category, limit)
    
    return jsonify({
        'results': results,
        'count': len(results),
        'query': query
    }), 200

@app.route('/api/categories', methods=['GET'])
def categories():
    """Get all available categories"""
    cats = get_all_categories()
    return jsonify({'categories': ['All'] + cats}), 200

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download a file"""
    try:
        filepath = os.path.join(Config.UPLOAD_FOLDER, secure_filename(filename))
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'running', 'message': 'API is healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
