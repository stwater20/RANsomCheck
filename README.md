# RANsomCheck

Ransomware attacks continue to evolve in complexity and sophistication, posing significant challenges to traditional detection methods. This project focuses on Windows Portable Executable (PE) files and employs dynamic analysis using Cuckoo Sandbox to generate execution reports, extracting API call sequences as key features for ransomware identification. 

We propose a deep learning-based detection model to address the rapidly evolving ransomware landscape. Two numerical representation methods are applied to process API calls, including direct conversion and quadruple-based semantic representation, which capture deeper relationships between API calls. Feature extraction utilizes embedding and convolution techniques to capture semantic relationships and structural patterns within API call sequences, enhancing the model's ability to identify ransomware behavior accurately. The Transformer model also analyzes the dependencies within API sequences to improve detection accuracy.

Our proposed model achieves:
- **Accuracy**: 99.94%
- **Precision**: 99.92%
- **Recall**: 100%
- **F1 Score**: 99.96%

Experimental results validate the model's reliability and effectiveness in ransomware detection. Furthermore, the methodology is implemented on a Web platform built with TypeScript, React, and Python Flask, enabling seamless file uploads for security analysis.

## Project Links

- **Frontend Repository**: [RANsomCheck-Frontend](https://github.com/Kiri487/RANsomCheck-Frontend)
- **Backend Repository**: [RANsomCheck-Backend](https://github.com/Shuan0402/RANsomCheck-Backend)
- **Model and Dataset**: [RANsomCheck-Data](https://github.com/Kiri487/RANsomCheck-Data)

## Additional Resources

- **Cuckoo Sandbox Installation and Usage Guide**: [HackMD Documentation](https://hackmd.io/@kiri487/112senior_project/https%3A%2F%2Fhackmd.io%2F%40jdcoj%2FBJLoyoQ7C)
