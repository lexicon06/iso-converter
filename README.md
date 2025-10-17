# 📀 ISO Creator

A modern and beautiful desktop application to convert folders into ISO files with an intuitive graphical interface.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

## ✨ Features

- 🎨 **Modern Dark UI** - Beautiful and professional interface
- 🌍 **Multi-language** - English and Spanish support
- 📁 **Easy to use** - Simple folder selection with browse buttons
- 🚀 **Fast processing** - Efficient ISO creation with progress tracking
- ⚙️ **Flexible options** - Include or exclude root folder in ISO
- 📊 **Real-time progress** - Visual progress bar with percentage
- ✅ **ISO 9660 compliant** - Full compatibility with Joliet and Rock Ridge extensions

## 🖼️ Screenshots

### English Interface
Clean and modern interface with all controls clearly labeled.

### Spanish Interface
Interfaz completamente traducida al español.

## 🔧 Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
- pycdlib

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/iso-creator.git
cd iso-creator
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python iso_creator.py
```

## 🚀 Usage

1. **Select Source Folder** - Click "Browse" next to "Source Folder" and select the folder you want to convert
2. **Select Output Folder** - Click "Browse" next to "Output Folder" and choose where to save the ISO
3. **Name your ISO** - Enter a name for your ISO file (default: MYCDROM)
4. **Optional: Include root folder** - Check this option if you want the source folder itself included in the ISO
5. **Generate ISO** - Click the "🚀 GENERATE ISO" button
6. **Wait for completion** - Watch the progress bar until it reaches 100%

## 🌐 Language Support

The application supports two languages:
- 🇬🇧 **English** (default)
- 🇪🇸 **Spanish**

Switch languages using the flag buttons in the top-right corner.

## ⚙️ Technical Details

### ISO Standards
- **ISO 9660** Level 3 compliance
- **Joliet** extension for long filenames (Windows)
- **Rock Ridge** 1.09 for POSIX file attributes (Unix/Linux)

### File Naming
- Automatically sanitizes filenames for ISO 9660 compatibility
- Converts invalid characters to underscores
- Maintains original names through Joliet extension

## 🛠️ Building Executable (Optional)

To create a standalone executable using PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="ISO Creator" iso_creator.py
```

The executable will be in the `dist` folder.

## 📋 Troubleshooting

### Common Issues

**Issue:** "Module not found" error
- **Solution:** Make sure you've installed all requirements: `pip install -r requirements.txt`

**Issue:** ISO file is empty or corrupted
- **Solution:** Verify the source folder exists and contains files

**Issue:** Application won't start on Linux
- **Solution:** Install tkinter: `sudo apt-get install python3-tk`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

Pablo Santillán - [@lexicon06](https://github.com/lexicon06)

## 🙏 Acknowledgments

- Built with [pycdlib](https://github.com/clalancette/pycdlib) - Pure Python ISO9660 library
- UI inspired by modern design principles
- Flag emojis for language selection

## 📧 Support

If you have any questions or need help, please open an issue on GitHub.

---

**Made with ❤️ and Python**
