#!/bin/bash
# MD to PDF converter using md-to-pdf (already installed globally)

convert_md_to_pdf() {
    local input_file="$1"
    local output_file="$2"

    if [ ! -f "$input_file" ]; then
        echo "Error: Input file '$input_file' not found"
        return 1
    fi

    # md-to-pdf always outputs to same name with .pdf extension
    md-to-pdf "$input_file"

    # Get the auto-generated filename
    local auto_output="${input_file%.md}.pdf"

    # If a custom output was specified and it's different, rename the file
    if [ -n "$output_file" ] && [ "$output_file" != "$auto_output" ]; then
        mv "$auto_output" "$output_file"
        echo "PDF generated: $output_file"
    else
        echo "PDF generated: $auto_output"
    fi
}

# If called directly with arguments
if [ "$#" -ge 1 ]; then
    convert_md_to_pdf "$@"
fi