# Sanctions Data Tool Set

## Issues
Relationships information extraction through sanctions vault and sanctions json not working...
Need to have both call the parse entity function from the same place to avoid any issues and ensure consistent 


## Goals
- CLI Operated program that can run three things:
    - Relationship Extraction
    - Vault Generation
    - JSON Entity Data  

## Structure 
```
main.py
    rel_extraction.py
    sanctions_json.py
    sanctions_vault.py
```


## Options 

| Option      | Flag | Options                   | Description              |
|-------------|------|---------------------------|--------------------------|
| Input File  | -i   | {sanctions_data.xml}      | Select a data source     |
| Output File | -o   | {output_file}             | Designate an output file |
| Function    | -f   | {relextract, vault, json} | Select functionality     |