# Streamlit UI for RAG Application

A beautiful, modern web interface for the RAG Document Assistant built with Streamlit.

## Features

### 🎨 Modern UI Design
- Clean, professional interface with gradient accents
- Responsive layout that works on all devices
- Custom styling with smooth animations
- Dark mode compatible

### 📥 Document Indexing
- Drag-and-drop PDF upload
- Multiple file upload support
- Real-time progress tracking
- Indexed document history with metadata

### 💬 Interactive Chat Interface
- Chat-style Q&A interface
- Conversation history
- Source document viewer with expandable sections
- Sample questions to get started

### 📊 Dashboard & Statistics
- Real-time metrics (indexed files, queries)
- Vector store status indicator
- Configuration management
- Clear chat history option

### 🔍 Advanced Features
- Toggle source document display
- Load existing vector stores
- Custom configuration file support
- API key status indicator

## Screenshots

### Chat Interface
The main chat interface allows you to ask questions about your indexed documents with an intuitive conversation flow.

### Document Indexing
Upload and index multiple PDF documents with real-time progress tracking and status updates.

### Source Documents
View source documents that were used to generate answers, including page numbers and content previews.

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
echo "OPENAI_API_KEY=sk-your-key-here" >> .env
```

### 3. Run the Application

```bash
streamlit run streamlit_app.py
```

The application will open in your default browser at `http://localhost:8501`

## Usage Guide

### Indexing Documents

1. Navigate to the **"Index Documents"** tab
2. Click **"Choose PDF files"** or drag-and-drop PDFs
3. Click **"🚀 Index Documents"** to process
4. Wait for the success message and balloons! 🎈

### Querying Documents

1. Go to the **"Chat & Query"** tab
2. Ensure vector store is loaded (green indicator in sidebar)
3. Type your question in the input field
4. Click **"🔍 Ask"** or press Enter
5. View the answer and optionally expand source documents

### Managing Configuration

**Sidebar Options:**
- **Configuration**: Change config file path and reload
- **Statistics**: View indexed files and query count
- **Options**: Toggle source document display
- **Clear History**: Reset chat conversation

## UI Components

### Layout Structure

```
┌─────────────────────────────────────────────┐
│           Header & Title                     │
├──────────┬──────────────────────────────────┤
│          │  Tab 1: Chat & Query             │
│ Sidebar  │  - Chat history                  │
│          │  - Query input                   │
│ - Config │  - Source viewer                 │
│ - Stats  │                                  │
│ - Options│  Tab 2: Index Documents          │
│          │  - File uploader                 │
│          │  - Index button                  │
│          │  - Document list                 │
└──────────┴──────────────────────────────────┘
```

### Color Scheme

- **Primary**: `#667eea` (Purple gradient)
- **Secondary**: `#764ba2` (Deep purple)
- **Success**: `#4CAF50` (Green)
- **Background**: `#ffffff` (White)
- **Secondary BG**: `#f0f2f6` (Light gray)
- **Text**: `#1e3a8a` (Dark blue)

## Customization

### Modify Theme

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#your-color"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#1e3a8a"
```

### Custom CSS

Edit the CSS in `streamlit_app.py` in the `st.markdown()` section:

```python
st.markdown("""
    <style>
    /* Your custom CSS here */
    </style>
""", unsafe_allow_html=True)
```

### Add New Features

The modular design makes it easy to extend:

1. **Add new tabs**: Create new tab functions
2. **Custom widgets**: Add Streamlit components
3. **Enhanced visualizations**: Use Plotly or Altair
4. **Export features**: Add download buttons for results

## Configuration Options

### Upload Limits

Default max upload size is 200MB. Change in `.streamlit/config.toml`:

```toml
[server]
maxUploadSize = 500  # in MB
```

### Session State Variables

The app uses these session state variables:
- `pipeline`: RAG pipeline instance
- `vectorstore_loaded`: Vector store status
- `chat_history`: Conversation history
- `indexed_files`: List of indexed documents
- `show_sources`: Source display toggle

## Troubleshooting

### Common Issues

**Problem**: Upload fails for large files
**Solution**: Increase `maxUploadSize` in config.toml

**Problem**: Slow performance with many documents
**Solution**: Reduce `chunk_size` in config.yaml or index fewer documents

**Problem**: CSS not applying
**Solution**: Clear browser cache and refresh (Ctrl+Shift+R)

**Problem**: Session state lost on refresh
**Solution**: This is expected - Streamlit resets on browser refresh

### Debug Mode

Run with debug logging:

```bash
streamlit run streamlit_app.py --logger.level=debug
```

## Deployment

### Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add secrets in Streamlit Cloud settings:
   ```toml
   OPENAI_API_KEY = "your-api-key"
   ```
5. Deploy!

### Deploy with Docker

```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.address", "0.0.0.0"]
```

Build and run:
```bash
docker build -t rag-streamlit .
docker run -p 8501:8501 -e OPENAI_API_KEY=your-key rag-streamlit
```

## Best Practices

1. **Clear chat regularly**: Long conversations can slow down the UI
2. **Index in batches**: Upload 5-10 documents at a time for best performance
3. **Use specific questions**: More specific queries yield better results
4. **Check sources**: Always review source documents for accuracy
5. **Monitor API usage**: Keep an eye on OpenAI API costs

## Advanced Features (Coming Soon)

- 📊 Document analytics dashboard
- 🎯 Advanced filtering options
- 📝 Export chat history
- 🔐 User authentication
- 📈 Query performance metrics
- 🌐 Multi-language support

## Contributing

To contribute new UI features:

1. Fork the repository
2. Create a feature branch
3. Add your Streamlit components
4. Test thoroughly
5. Submit a pull request

## Support

For issues specific to the Streamlit UI:
- Check the [Streamlit documentation](https://docs.streamlit.io)
- Review [Streamlit community forum](https://discuss.streamlit.io)
- Open an issue on GitHub

## License

MIT License - same as the main RAG application