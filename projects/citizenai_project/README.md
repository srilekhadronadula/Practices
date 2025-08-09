# 🏛️ Citizen AI - Intelligent Citizen Engagement Platform
#DEMO LINK — https://drive.google.com/file/d/1_hH7heXPRDoqBguDOm5Q2LE-HdWff2RP/view?usp=sharing

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Gradio](https://img.shields.io/badge/Gradio-4.0%2B-orange.svg)](https://gradio.app)
[![IBM Granite](https://img.shields.io/badge/AI%20Model-IBM%20Granite%203.0--2B-green.svg)](https://huggingface.co/ibm-granite)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An AI-powered platform designed to bridge the gap between citizens and government services in India. Built with IBM Granite 3.0-2B local AI model and modern web technologies to provide intelligent, accessible, and efficient citizen engagement solutions.

## 🌟 Features

### 🤖 AI-Powered Assistant
- **Local AI Model**: IBM Granite 3.3-2B running locally for privacy and offline capability
- **Conversational Interface**: Natural language interaction for government service queries
- **Context-Aware Responses**: Understands Indian government schemes, processes, and services
- **Multi-language Support**: Designed for Indian citizen needs

### 👤 Citizen Dashboard
- **Personal Profile Management**: Store citizen information securely
- **Real-time Notifications**: Government alerts, scheme updates, and service announcements
- **Region-specific Information**: Localized content based on user location

### 📝 Feedback & Complaints System
- **Intelligent Complaint Registration**: Categorized complaint system with unique IDs
- **Sentiment Analysis**: Automatic sentiment detection for citizen feedback
- **Status Tracking**: Real-time complaint status updates
- **Analytics Dashboard**: Visual insights into citizen satisfaction

### 🏛️ Government Services Guide
- **Step-by-step Guides**: Detailed instructions for essential services
  - Ration Card Application
  - Birth Certificate
  - Pension Schemes
  - Voter ID Registration
  - PAN Card Application
  - Passport Services

### 📋 AI Document Generator
- **RTI Applications**: Auto-generate Right to Information requests
- **Complaint Letters**: Formal complaint letter templates
- **Application Forms**: Government service application drafts
- **Policy Summaries**: AI-powered policy document summarization

### 📊 Analytics & Insights
- **Sentiment Tracking**: Monitor citizen satisfaction trends
- **Complaint Analytics**: Visual dashboard for complaint status and categories
- **Engagement Metrics**: Track platform usage and citizen participation

### 🗳️ Participatory Governance
- **Public Polling**: Digital voting on civic issues
- **Discussion Forums**: Community engagement on local topics
- **Feedback Collection**: Structured citizen input mechanisms

### ⚙️ Admin Panel
- **Government Dashboard**: Administrative interface for officials
- **Complaint Management**: Update and track complaint resolution
- **Broadcast System**: Send notifications to all citizens
- **Usage Analytics**: Platform statistics and user engagement data

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- CUDA-compatible GPU (optional, for better performance)
- 8GB+ RAM recommended
- Internet connection for initial model download

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/citizen-ai.git
   cd citizen-ai
   ```

2. **Install Dependencies**
   ```bash
   pip install gradio>=4.0.0 pandas>=1.5.0 plotly>=5.15.0 textblob>=0.17.1
   pip install numpy>=1.21.0 python-dateutil>=2.8.2
   pip install transformers>=4.35.0 torch>=2.0.0 accelerate>=0.20.0 bitsandbytes>=0.41.0
   ```

3. **Run the Application**
   ```bash
   python CITIZENAI.py
   ```

4. **Access the Platform**
   - Local: `http://localhost:7860`
   - Public link will be generated automatically

## 🔧 Configuration

### Environment Setup

The application automatically detects your system capabilities:
- **GPU Available**: Uses CUDA optimization with 8-bit quantization
- **CPU Only**: Falls back to CPU processing with FP32 precision

### Model Configuration

```python
MODEL_NAME = "ibm-granite/granite-3.3-2b-instruct"
device = "cuda" if torch.cuda.is_available() else "cpu"
```

### Customization Options

- **Region Settings**: Modify the region dropdown in the citizen dashboard
- **Service Categories**: Add new complaint categories in the feedback system
- **Notification Types**: Customize alert types and messaging
- **Language Support**: Extend prompts for regional languages

## 📱 Usage Guide

### For Citizens

1. **Start with AI Assistant**: Ask questions about government services
2. **Create Profile**: Register your information in the Citizen Dashboard
3. **Submit Feedback**: Share experiences with government services
4. **File Complaints**: Register issues with automatic tracking
5. **Generate Documents**: Create RTI applications and complaint letters
6. **Participate**: Engage in polls and community discussions

### For Government Officials

1. **Access Admin Panel**: Monitor citizen engagement and complaints
2. **Manage Complaints**: Update status and track resolution progress
3. **Send Notifications**: Broadcast important updates to citizens
4. **Analyze Data**: Review sentiment trends and service feedback
5. **Generate Reports**: Export analytics for policy decisions

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   AI Engine      │    │   Data Layer    │
│   (Gradio)      │◄──►│   (IBM Granite)  │◄──►│   (In-Memory)   │
├─────────────────┤    ├──────────────────┤    ├─────────────────┤
│ • Chat Interface│    │ • Text Generation│    │ • User Profiles │
│ • Dashboards    │    │ • Sentiment Anal.│    │ • Complaints    │
│ • Forms         │    │ • Document Gen.  │    │ • Feedback      │
│ • Analytics     │    │ • Summarization  │    │ • Analytics     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🔐 Security & Privacy

- **Local AI Processing**: No data sent to external AI services
- **In-Memory Storage**: Data stored locally during session
- **Privacy by Design**: Minimal data collection and processing
- **Secure Communication**: HTTPS support for production deployment

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include error handling for all user inputs
- Test on both GPU and CPU environments
- Update documentation for new features

## 📋 Roadmap

- [ ] **Multi-language Support**: Hindi, Tamil, Telugu, Bengali
- [ ] **Voice Interface**: Speech-to-text and text-to-speech
- [ ] **Mobile App**: React Native mobile application
- [ ] **Database Integration**: PostgreSQL/MongoDB support
- [ ] **API Development**: RESTful API for third-party integration
- [ ] **Advanced Analytics**: Machine learning insights
- [ ] **Blockchain Integration**: Secure document verification
- [ ] **Video Chat**: Live support with government officials

## 🐛 Known Issues

- **Memory Usage**: High RAM consumption with large conversations
- **Model Loading**: Initial startup time can be 2-5 minutes
- **GPU Memory**: CUDA out of memory errors with small GPUs (<6GB)
- **Browser Compatibility**: Some features may not work in older browsers

## 📚 Documentation

- [User Guide](docs/user-guide.md)
- [Admin Manual](docs/admin-manual.md)
- [API Reference](docs/api-reference.md)
- [Deployment Guide](docs/deployment.md)

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/citizen-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/citizen-ai/discussions)
- **Email**: support@citizen-ai.example.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **IBM Research**: For the Granite AI model
- **Gradio Team**: For the excellent web framework
- **Hugging Face**: For model hosting and transformers library
- **Indian Government**: For digital governance initiatives
- **Open Source Community**: For various supporting libraries

## 📊 Statistics

- **Languages**: Python, JavaScript, HTML, CSS
- **AI Model**: IBM Granite 3.0-2B (2.6B parameters)
- **Framework**: Gradio 4.0+
- **Supported Platforms**: Linux, Windows, macOS
- **Deployment**: Local, Google Colab, Cloud platforms


## 📞 Contact

- **Project Lead**: DRONADULA SRILEKHA


---

<div align="center">
  <strong>🏛️ Empowering Citizens Through AI-Driven Governance Solutions</strong>
  <br>
  Made with ❤️ for Digital India Initiative
</div>
