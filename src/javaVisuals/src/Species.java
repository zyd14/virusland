import java.util.ArrayList;

//Structure to create a Species
public class Species {

	String accessionNumber;
	String name;
	ArrayList<Protein> proteinList;

	public Species(String accessionNumber, String name) {
		this.accessionNumber = accessionNumber;
		this.name = name;
		this.proteinList = new ArrayList<Protein>();
	}


	public String getAccessionNumber() {
		return accessionNumber;
	}

	public String getName() {
		return name;
	}

	public int getTotalNumberOfProteins() {
		return this.proteinList.size();
	}

	
	public void addProtein(String accessionNumber, int numberOfHits){
		Protein protein = new Protein(accessionNumber,numberOfHits);
		this.proteinList.add(protein);
	}

}
