use std::env;
use std::fs;

use directory_catalogue::run;

fn main() {
    println!("DIRECTORY CATALOGUE");

    let args: Vec<String> = env::args().collect();
    if args.len() < 2{
        eprintln!("FAILED: No input path given.");
        std::process::exit(1);
    }

    let target_path = fs::canonicalize(&args[1]).unwrap_or_else(|_|{
        eprintln!("FAILED: input path cannot be read.");
        std::process::exit(1);
    });

    if !target_path.is_dir() {
        eprintln!("FAILED: input path is not a directory.");
        std::process::exit(1);
    }

    run(&target_path);   
}
