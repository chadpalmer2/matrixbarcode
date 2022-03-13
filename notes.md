# Notes on my senior project

## Timeline

- By 3/16
    - Learn entirely of mathematical grounding of Reed-Solomon encoding to presentation level
    - Build Reed-Solomon encoder in JavaScript with simple front-end
    - Design barcode
- By 4/6
    - Have very basic encoder/decoder implemented in JavaScript
- By 4/20
    - Improve decoder:
        - Transformations for "real-world" skewed and damaged images
        - Varied sizes for payloads of multiple sizes
    - Framework for mobile application
- By 5/4
    - Finalize, clean up code, write whitepaper

## Ideas

### Flow of data through coding and decoding

- Coding (data to model to image)
    - Data is encoded in binary
    - Data is encoded utilizing Reed-Solomon encoding
    - Data is incorporated into model
    - Model is exported as image
- Decoding (heavily QR inspired)
    - (image to model)
        - Image is captured
        - Finder patterns determine axis of orientation, timer patterns determine skew
        - Math is done to determine where each module is
        - Modules are iterated over to determine theoretic matrix version of code
        - Subsets of pixels associated with given module are determined, average color value taken to determine bit value
    - (model to image)
        - Data is decoded utilizing Reed-Solomon encoding
        - Payload displayed

### Mathematical presentation

- Build up Reed-Solomon encryption from the theoretical ground up
    - Information theory
    - Codes
    - Hamming codes
    - ???

### Single app design

- Sufficiently well-developed mobile site for encoding and decoding data
    - Incorporate photo taking and upload feature onto website

## Resources

[QR Code documentation - ISO standard](https://github.com/yansikeim/QR-Code/blob/master/ISO%20IEC%2018004%202015%20Standard.pdf)

[QR Code Generator in multiple langauges](https://github.com/kazuhikoarase/qrcode-generator)

## Meeting notes

- packages to run javascript on command line for development
    - node.js would be really nice for bundling front-end and back-end
    - automatic packaging into a mobile application
- reed-solomon encoding probably sufficiently complex for presentation, no need for additional information theory
