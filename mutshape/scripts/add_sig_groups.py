import pandas as pd
import sys

# Mapping of signatures to their corresponding groups
signature_groups = {
    "Clock": ["SBS1", "SBS5"],
    "APOBEC": ["SBS2", "SBS13"],
    "HR_Deficiency": ["SBS3"],
    "Tobacco": ["SBS4", "SBS29", "SBS92"],
    "MMR_Deficiency": ["SBS6", "SBS14", "SBS15", "SBS20", "SBS21", "SBS26", "SBS44"],
    "UV": ["SBS7a", "SBS7b", "SBS7c", "SBS7d", "SBS38"],
    "Unknown": ["SBS8", "SBS12", "SBS16", "SBS17a", "SBS17b", "SBS19", "SBS23", "SBS28", 
                "SBS33", "SBS34", "SBS37", "SBS39", "SBS40a", "SBS40b", "SBS40c", "SBS41", 
                "SBS89", "SBS91", "SBS93", "SBS94", "SBS96", "SBS97", "SBS98"],
    "Lymphoid": ["SBS9", "SBS84", "SBS85"],
    "POL_Deficiency": ["SBS10a", "SBS10b", "SBS10c", "SBS10d"],
    "Chemotherapy_Treatment": ["SBS11", "SBS25", "SBS31", "SBS32", "SBS35", "SBS86", 
                               "SBS87", "SBS90", "SBS99"],
    "ROS": ["SBS18"],
    "AA": ["SBS22a", "SBS22b"],
    "Aflatoxin": ["SBS24"],
    "BER_Deficiency": ["SBS30", "SBS36"],
    "Haloalkane": ["SBS42"],
    "Colbactin": ["SBS88"],
    "Possible_Seq_Artifact": ["SBS27", "SBS43", "SBS45", "SBS46", "SBS47", "SBS48", "SBS49", 
                              "SBS50", "SBS51", "SBS52", "SBS53", "SBS54", "SBS55", "SBS56", 
                              "SBS57", "SBS58", "SBS59", "SBS60", "SBS95"]
}

def map_signature_group(csv_file):
    # Load the CSV file
    df = pd.read_csv(csv_file)

    # Ensure "Signature" column exists
    if "Signature" not in df.columns:
        raise ValueError("Error: The CSV must contain a 'Signature' column.")

    # Create a mapping dictionary for fast lookup
    signature_to_group = {sig: group for group, sigs in signature_groups.items() for sig in sigs}

    # Map each row's Signature to its group, default to "Unknown" if not found
    df["Signature_Group"] = df["Signature"].map(signature_to_group).fillna("Unknown")

    # Save the updated DataFrame back to the same file
    df.to_csv(csv_file, index=False)
    print(f"Updated CSV saved to: {csv_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python collapse_sigs.py <csv_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    map_signature_group(csv_file)
