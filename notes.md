# Notes on my senior project

## Timeline

- By 4/13
    - Have math presentation materials complete
    - Have super barebones encoder and decoder complete: think minimum viable product
- By 4/27
    - Have presentation done
    - Clean up website and add quality of life features, improve functionality
- By 5/4
    - Finalize everything, produce whitepaper write-up

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

### Sufficient data storage with simple snowflake design
Sufficient: 75 ASCII characters, 75 bytes, 600 bits

$600 * 1.5 = 900$ bits

Consider: 12 sets of 24 lines of 8 length gradations
Consider: 

Calculation: $\log_2(8^{12 * 24}) = 864$, 864 bits of data storage

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

[JS image processing](https://webkid.io/blog/image-processing-in-javascript/)

[RS encoder/decoder in Python3](https://github.com/tomerfiliba/reedsolomon)

## Meeting notes

- packages to run javascript on command line for development
    - node.js would be really nice for bundling front-end and back-end
    - automatic packaging into a mobile application
- reed-solomon encoding probably sufficiently complex for presentation, no need for additional information theory
