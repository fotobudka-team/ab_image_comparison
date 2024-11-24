# Anotation tool for A/B Image Comparison

This repository provides an image annotation tool built with Streamlit for A/B image comparisons. The tool allows users to compare two images side by side and select the one that better fits their requirements. It avoids duplications and helps efficiently create annotated data for training machine learning models.

---

## Features

- **Efficient Workflow**: Pre-generated annotation pairs ensure smooth and fast annotation.
- **Duplicate-Free Comparisons**: Avoid repeated annotations for the same image pairs.
- **Multi-Project Support**: Manage and switch between multiple projects with ease.
- **Custom Pair Generation**: Supports random pair generation with future plans for dense and user-specific pairs.
- **Keyboard Shortcuts**: Annotate quickly using left and right arrow keys for selections.

---

## Required directory structure
The tool requires a specific directory structure for input images and annotations. Input images should be placed in a subdirectory within the `data` directory, which is also used to store the resulting annotations. After cloning the repository, your directory structure should look like this:

```
├── data
│   ├── input
|   |   ├── image_1234.jpg
|   |   ├── image_5678.jpg
|   |   ├── ...
├── pages
│   ├── annotate.py
│   ├── ...
├── .gitignore
├── Dockefile
├── ...
```

## How it works
### 1. Create a Project
You can manage multiple projects in the app. To create a project, provide the following:
- **Project Name**: A unique name for the project.
- **Input Directory**: Directory containing source images.
- **Output Directory**: Unique directory where annotations will be saved.

Project configurations are saved in the `configs` directory. After creating your first project, the directory structure will be updated as follows:


```
├── configs
│   ├── project_name.json
├── data
│   ├── ...
├── pages
│   ├── ...
├── ...
```
Example configuration file (`project_name.json`).
```json
{
    "name": "Portrait", 
    "input": "./data/input", 
    "output": "./data/output"
}
```

### 2. Continue an Existing Project
Select a previously saved project from the list to resume annotating or generating annotation pairs. Projects must be selected before performing any operations.

### 3. Create pairs
Before annotating, generate annotation pairs. These are stored in the `./data/defined_output/` to_annotate directory. Each annotation pair is saved as a JSON file in this format:
File name:
```
image_1234_image_5678.json
```
Example content:
```json
{
    "img_a": "image_1234.jpg", 
    "img_b": "image_5678.jpg", 
    "annotation": None, 
    "author": None, 
    "date": None
}
```

**Why Pre-Generate Pairs?**
Pre-generating pairs ensures:

* Faster annotations without on-the-fly generation.
* No duplicate comparisons.
* Scalability for future features like dense pair generation or user-specific assignments.

### 4. Annotate
The annotation interface shows:

* The count of remaining annotations.
* Two images displayed side by side.

You can select the better image by clicking `A` or `B` or by pressing the left or right arrow keys. Each annotation is saved in the `./data/defined_output/annotations` directory with the following metadata:

* Label: `0` (for Image A) or `1` (for Image B).
* Timestamp: Current date and time.
* Author: Retrieved from `os.environ.get("USER")`.

## License
This project is licensed under the Non-Commercial License.

## Contributing
Contributions are welcome! If you encounter issues or have feature requests, feel free to open an issue or submit a pull request.