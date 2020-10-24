use std::fs;
use std::fs::File;
use std::io::prelude::*;
use std::path::PathBuf;
use toml::Value;

struct Page {
    name: String,
    title: String,
    children: Vec<Page>,
    info: Option<toml::Value>
}

impl std::fmt::Display for Page {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.name)
    }
}

fn get_page_name(path: &PathBuf) -> String{
    String::from(path.file_name().unwrap().to_str().unwrap())
}

// fn get_extension(path: &PathBuf) -> String{
//     String::from(path.extension().unwrap().to_str().unwrap())
// }

fn build_page(path: &PathBuf, is_root: bool) -> Page {
    let mut children_path = Vec::<PathBuf>::new();
    let mut info: Option<toml::Value> = None;

    for item in fs::read_dir(path).expect("FAILED: Cannot read content of input path."){
        if let Ok(item) = item {
            let item_path = item.path();

            if item_path.is_dir(){
                if !item_path.ends_with("catalogue"){
                    children_path.push(item_path.clone());
                }
            }
            
            if item_path.ends_with("info.toml"){
                println!("Found TOML file");

                let mut file = File::open(item_path).expect("FAILED: Cannot open toml file.");
                let mut contents = String::new();
                file.read_to_string(&mut contents).expect("FAILED: Cannot read toml file.");
                info = Some(contents.parse::<Value>().expect("FAILED: Invalid toml file in {}"));
            }
        }
    }

    let page_name = if is_root {
        String::from("root")
    }else{
        get_page_name(path)
    };

    let title = if is_root {
        String::from("Root Directory")
    }else{
        match &info {
            Some(data) => String::from(data["title"].as_str().unwrap()),
            None => page_name.clone()
        }
    };

    // build child pages
    let mut children_pages = Vec::<Page>::new();

    for sub_path in children_path{
        children_pages.push(build_page(&sub_path, false));
    }

    Page {
        name: page_name,
        title: title,
        children: children_pages,
        info: info
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

    // build directory pages
    create_default_page(page, &dir_path)?;

    Ok(())
}

fn create_default_page(page: &Page, parent_path: &PathBuf) -> std::io::Result<()> {
    println!("Building page: {}", page);
    if !parent_path.exists() {
        fs::create_dir_all(&parent_path)?;
    }

    let mut output_file = File::create(&parent_path.join("Readme.md"))?;
    let mut output_page = format!("# {}\n\n", page.title);

    // add links to children page
    if page.children.len() > 0 {
        output_page.push_str("## Sub-directories\n\n");
        for sub_page in &page.children{
            output_page.push_str(format!("[{}]({})\n\n", sub_page.title, sub_page.name).as_str());
        }
    }

    // add infomation in info.toml
    let info = &page.info;
    if info.is_some() {
        let data = info.clone().unwrap();
        output_page.push_str("## Description\n\n");
        output_page.push_str(format!("{}\n\n", data["description"].as_str().unwrap()).as_str());
    }

    output_file.write_all(output_page.as_bytes())?;

    // create children pages recursively
    for sub_page in &page.children{
        create_default_page(&sub_page, &parent_path.join(&sub_page.name))?;
    }

    Ok(())
}

pub fn run(root_path: &PathBuf){

    // let mut pages = Vec::<Page>::new();
    
    println!("Constructing directory tree on root: {}", root_path.display());

    // build pages
    let root_page = build_page(&root_path, true);

    // create default output
    create_default_output(&root_page, &root_path).expect("FAILED: Cannot successfully create output catalogue.");

}