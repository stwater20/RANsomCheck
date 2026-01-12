# RANsomCheck: A CNN-Transformer Model for Malware Detection Based on API Call Sequences

Ransomware attacks are becoming increasingly complex and sophisticated, posing significant challenges to traditional detection methods. This study focuses on Windows Portable Executable (PE) files and leverages dynamic analysis with Cuckoo Sandbox to generate execution reports, identifying critical features for ransomware detection through API call sequences. To address the rapidly evolving ransomware landscape, we propose a deep learning-based detection model that employs two numerical representation methods for processing API calls: direct conversion and a novel quadruple-based semantic representation, which effectively captures deeper relationships between API calls. Our approach integrates embedding and convolutional techniques to extract semantic relationships and structural patterns from API call sequences, enhancing the model's ability to recognize ransomware behaviors with high precision. Additionally, the Transformer model is employed to analyze sequence dependencies, further improving detection accuracy. The proposed model demonstrates remarkable performance, achieving an accuracy of 99.94%, precision of 99.92%, recall of 100%, and an F1 score of 99.96%, highlighting its reliability and effectiveness. Furthermore, we developed a web-based platform using TypeScript, React, and Python Flask, enabling seamless file uploads and comprehensive security analysis.

## Project Links

- **Frontend Repository**: [RANsomCheck-Frontend](https://github.com/Kiri487/RANsomCheck-Frontend)
- **Backend Repository**: [RANsomCheck-Backend](https://github.com/Shuan0402/RANsomCheck-Backend)
- **Model and Dataset**: [RANsomCheck-Data](https://github.com/Kiri487/RANsomCheck-Data)

## Additional Resources

- **Cuckoo Sandbox Installation and Usage Guide**: [HackMD Documentation](https://hackmd.io/@jdcoj/BJLoyoQ7C)

## Citation

Chen, S. S., Wu, Y. X., Ho, Y. X., Cheng, P. P., & Sun, C. Y. (2025, July). RANsomCheck: A CNN-Transformer Model for Malware Detection Based on API Call Sequences. In International Conference on Industrial, Engineering and Other Applications of Applied Intelligent Systems (pp. 116-127). Singapore: Springer Nature Singapore.


## Acknowledgements

Special thanks to [Han-Xuan Huang](https://github.com/ntut-xuan) for serving as an technical advisor and providing valuable assistance in system development.
