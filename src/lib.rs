use std::fs;
use std::fs::File;
use std::io::prelude::*;
use std::path::PathBuf;

struct Page {
    name: String,
    children: Vec<Page>
}

impl std::fmt::Display for Page {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.name)
    }
}

fn get_page_name(path: &PathBuf) -> String{
    String::from(path.file_name().unwrap().to_str().unwrap())
}

fn get_extension(path: &PathBuf) -> String{
    String::from(path.extension().unwrap().to_str().unwrap())
}

fn build_page(path: &PathBuf, is_root: bool) -> Page {
    let mut children_path = Vec::<PathBuf>::new();

    for item in fs::read_dir(path).expect("FAILED: Cannot read content of input path."){
        if let Ok(item) = item {
            let item_path = item.path();

            if item_path.is_dir(){
                children_path.push(item_path);
            }else{
                if get_extension(&item_path) == "toml"{
                    println!("Found TOML file")
                }
            }
        }
    }

    let page_name = if is_root {
        String::from("root")
    }else{
        get_page_name(path)
    };

    // build child pages
    let mut children_pages = Vec::<Page>::new();

    for sub_path in children_path{
        children_pages.push(build_page(&sub_path, false));
    }

    Page {
        name: page_name,
        children: children_pages
    }
}

fn create_default_output(page: &Page, root_path: &PathBuf) -> std::io::Result<()> {
    let mut output_path = root_path.clone();
    output_path.push("catalogue");
    output_path.push("md");

    // clear previous output
    println!("Create default output (Markdown stack) at {}", output_path.display());
    if output_path.exists(){
        fs::remove_dir_all(&output_path)?;
    }
    fs::create_dir_all(&output_path)?;

    // create home page
    let fav_path = output_path.clone().join("favourite");
    let tag_path = output_path.clone().join("tags");
    let dir_path = output_path.clone().join("directory");

    fs::create_dir(&fav_path)?;
    fs::create_dir(&tag_path)?;
    fs::create_dir(&dir_path)?;

    let mut output_file = File::create(output_path.clone().join("Readme.md"))?;
    let mut output_page = format!("# Directory Catalogue\n\n");
    output_page.push_str("[Favourite](favourite)\n\n");
    output_page.push_str("[Tags](tags)\n\n");
    output_page.push_str("[Directory](directory)\n\n");

    output_file.write_all(output_page.as_bytes())?;

    // // print page tree
    // for page in pages{
    //     println!("Page: {}", page);
    //     // let mut output_file: File;
    //     // let mut output_page: String;
    //     // if page.name == "root"{
    //     //     output_file = File::create(&dir_path.clone().join("Readme.md"))?;
    //     //     output_page = format!("# Root directory\n\n");
    //     // }else{
    //     //     output_file = File::create(&dir_path.clone().join(&page.name).join("Readme.md"))?;
    //     //     output_page = format!("# {}\n\n", &page.name);
    //     // }

    //     for sub_page in &page.children{
    //         println!("      --{}", sub_page.display());

    //         // output_page.push_str("[{}]({})")
    //     }
    // }

    Ok(())
}

pub fn run(root_path: &PathBuf){

    // let mut pages = Vec::<Page>::new();
    
    println!("Working on root: {}", root_path.display());

    // build pages
    let root_page = build_page(&root_path, true);

    // create default output
    create_default_output(&root_page, &root_path).expect("FAILED: Cannot successfully create output catalogue.");

}