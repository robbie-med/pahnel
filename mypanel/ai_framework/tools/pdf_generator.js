const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');

function generatePDF(mdFile, outputFile = null) {
    const autoOutput = mdFile.replace('.md', '.pdf');
    const finalOutput = outputFile || autoOutput;

    return new Promise((resolve, reject) => {
        // md-to-pdf always outputs to same name with .pdf extension
        exec(`md-to-pdf "${mdFile}"`, (error, stdout, stderr) => {
            if (error) {
                reject(`Error: ${error.message}`);
                return;
            }

            // If custom output specified and different, rename the file
            if (outputFile && outputFile !== autoOutput) {
                fs.rename(autoOutput, finalOutput, (err) => {
                    if (err) {
                        reject(`Error renaming file: ${err.message}`);
                        return;
                    }
                    resolve(`PDF created: ${finalOutput}`);
                });
            } else {
                resolve(`PDF created: ${autoOutput}`);
            }
        });
    });
}

module.exports = { generatePDF };