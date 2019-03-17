import CITS2200.Sort;

/**
* Sorting array using insertionSort, MergeSort, and QuickSort
* @author Shikai Wang StudentID:21938451
**/

public class Sorter implements Sort
{
   private int count;
   
   /**
	* Returns the number of array assignment operations 
	* performed by this class since the count variable was rest.
	* @return the number of assignments
	**/
	public int getCount(){
		return count;
	}	
		
	/**
	*Resets the counter variable to 0
	**/
	public void reset(){
		count = 0;
	}
	
	/**
	* Executes the insertion sort algorithm sorting the argument array.
	* There is no return as the parameter is to be mutated.
	* @param a the array of long integers to be sorted
	**/
	public void insertionSort(long[] a)
    	{
		for(int j=1; j<a.length; j++) {
			
			long num = a[j];
			int i = j - 1;
			while(i >=0 && a[i] > num) {
				
				a[i+1] = a[i];
				i = i - 1;
				count++;
				
				}
			a[i+1] = num;
			}
    	}
		
	/**
	* Executes the quick sort algorithm sorting the argument array.
	* There is no return as the parameter is to be mutated.
	* @param a the array of long integers to be sorted
	**/
	public void quickSort(long[] a){
		quickSort(a, 0, a.length-1);
	}
	
	private void quickSort(long a[], int p, int r) {

		if(p<r) {
			int q = partition(a, p, r);
			quickSort(a, p, q-1);
			quickSort(a, q+1, r);
		}
	}
	
	private int partition(long a[], int p, int r) {
		long x = a[r];
		int i = p - 1;
		for(int j=p; j<=r-1; j++) {
			if(a[j] <= x) { 
				i++;
				long temp = a[i];
				a[i] = a[j];
				a[j] = temp;
			}
			count++;
		}
		long temp = a[i+1];
		a[i+1] = a[r];
		a[r] = temp;
		return i + 1;
	}
	
	
	/**
	* Executes the merge sort algorithm sorting the argument array.
	* There is no return as the parameter is to be mutated.
	* @param a the array of long integers to be sorted
	**/
	public void mergeSort(long[] a){
	mergeSort(a, 0, a.length-1);
	}
	

	private void merge(long[] a, int p, int q, int r)
	{
	int n = q-p+1;
	int m = r-q;
	long[] an = new long[n];
	long[] am = new long[m];
	for(int i = 0; i<n; i++) {
	an[i] = a[p+i];
	count++;
	}
	for(int i = 0; i<m; i++){
	am[i] = a[q+i+1];
	count++;
	}
	int i = 0;
	int j = 0;
	for(int k = p; k<=r; k++){
	if(i==n) a[k] = am[j++];
	else if(j==m || an[i]<am[j]) a[k] = an[i++];
	else a[k] = am[j++];
	count++;
	}
	}
	
   /**
   *Overloads the mergeSort method with parameters to set the 
   *range to be sorted.
   **/ 
	private void mergeSort(long[] a, int p, int r)
	{
	if(p<r){
	int i = (p+r)/2;
	mergeSort(a,p,i);
	mergeSort(a,i+1,r);
	merge(a, p,i,r);
	}
	}
	
  
  }