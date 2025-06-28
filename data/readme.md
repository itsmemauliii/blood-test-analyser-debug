# 🩸 Blood Test Analysis System

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green.svg)
![CrewAI](https://img.shields.io/badge/CrewAI-0.28-orange.svg)

## 📂 Data Folder Structure

```
data/
├── default_reports/          # Pre-loaded sample reports
│   ├── blood_test_report.pdf  # Primary comprehensive report
│   └── sample.pdf             # Secondary sample report
└── system_uploads/           # Auto-created for user uploads
```

## 📄 Included Sample Reports

### 1. `blood_test_report.pdf`
- **Size**: 688 KB
- **Contents**:
  - Complete blood count (CBC)
  - Liver & kidney function tests
  - Lipid profile
  - Thyroid panel
  - Vitamin levels (B12, D)
- **Best For**: Testing full analysis capabilities

### 2. `sample.pdf` 
- **Size**: 688 KB  
- **Contents**: (Similar structure as above)
- **Best For**: Quick testing and development

## 🛠️ How to Use Existing Files

### Accessing Samples Programmatically
```python
from utils.file_manager import FileManager

manager = FileManager()

# Get primary sample
primary_report = manager.get_sample_report()  # returns blood_test_report.pdf

# Get specific sample
secondary_report = manager.get_sample_report("sample.pdf")
```

### API Endpoints
```http
POST /analyze
Body:
- file: (optional) PDF upload
- use_sample: true/false (defaults to blood_test_report.pdf if no file)
```

## 🔄 System Workflow

1. When no file is uploaded:
   ```mermaid
   graph LR
     A[API Request] --> B{File Provided?}
     B -->|No| C[Use blood_test_report.pdf]
     C --> D[Process Analysis]
   ```

2. With file upload:
   ```mermaid
   graph LR
     A[API Request] --> B[Save to system_uploads/]
     B --> C[Process Analysis]
     C --> D[Cleanup after 24h]
   ```

## 🧪 Testing with Included Samples

### Python Example
```python
# Test with default sample
from main import run_crew
from utils.file_manager import FileManager

report_path = FileManager().get_sample_report()
result = run_crew("Analyze CBC", str(report_path))
```

### cURL Example
```bash
# Use built-in sample
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "use_sample=true" \
  -F "query=Analyze%20my%20blood%20test"
```

## 🧹 Maintenance

- User uploads in `system_uploads/` are automatically cleaned up
- Default reports remain unchanged
- To add new sample reports:
  1. Place PDFs in `default_reports/`
  2. Update this README

## ⚠️ Important Notes

1. These sample reports contain synthetic data - no real patient information
2. Both sample files are 688KB but contain different test cases
3. For production:
   - Replace samples with your own reports
   - Set appropriate retention policies

Key features of this README:

1. **Clear Visualization** of your existing two-file setup
2. **Specific Documentation** for each sample PDF
3. **Usage Examples** for both programmatic and API access
4. **Workflow Diagrams** showing how the system handles samples
5. **Maintenance Guidelines** for the data layer
6. **Testing Recipes** to immediately work with your files
