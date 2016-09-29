
//Structure to create a protein
public class Protein {

	String accessionNumber;
	int numberOfHits;
	
	public Protein(String accessionNumber, int numberOfHits){
		this.accessionNumber = accessionNumber;
		this.numberOfHits = numberOfHits;
	}

	public String getAccessionNumber() {
		return accessionNumber;
	}

	public int getNumberOfHits() {
		return numberOfHits;
	}
	
	
}
