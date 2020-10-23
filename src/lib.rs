use std::fs;
use std::path::PathBuf;

struct Page {
    name: String,
    children: Vec<PathBuf>
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

fn build_page(pages: &mut Vec<Page>, path: &PathBuf, is_root: bool) -> () {
    let mut children_pages = Vec::<PathBuf>::new();

    for item in fs::read_dir(path).expect("FAILED: Cannot read content of input path."){
        if let Ok(item) = item {
            children_pages.push(item.path());
        }
    }

    let page_name = if is_root {
        String::from("root")
    }else{
        get_page_name(path)
    };

    let new_page = Page {
        name: page_name,
        children: children_pages.clone()
    };

    pages.push(new_page);

    // build child pages
    for sub_path in children_pages{
        if sub_path.is_dir() {
            build_page(pages, &sub_path, false);
        } else{
            if get_extension(&sub_path) == "toml"{
                println!("Found TOML file")
            }
        }
        
    }
}

pub fn run(root_path: &PathBuf){

    let mut pages = Vec::<Page>::new();
    
    println!("Working on root: {}", root_path.display());

    // add root page
    build_page(&mut pages, root_path, true);

    // print page tree
    for page in pages{
        println!("Page: {}", page);
        for sub_page in page.children{
            println!("      --{}", sub_page.display());
        }
    }

}