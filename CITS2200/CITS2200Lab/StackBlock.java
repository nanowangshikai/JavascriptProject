import CITS2200.Stack;
import CITS2200.Underflow;
import CITS2200.Overflow;

/**
 * This is stackblock to push and pop element also check error
 * @author Shikai Wang  studentID:21938451
 */
public class StackBlock implements Stack {
	int poi = 0;
	Object[] stack;
	int s;

	/**
	 * initialise object stack
	 * @param pass int s
	 */
	public StackBlock(int s) {
		if(s<1){
			throw new IllegalArgumentException("size of s is less than 1 and now is: "+ s);
		}
		stack = new Object[s];
		this.s = s;
	}
	/**
	 * Check if it is empty
	 * @return return if it is empty
	 */
	public boolean isEmpty() {
		return (poi == 0);
	}
	
	/**
	 * check if it is full
	 * @return return boolean if it is full
	 */
	public boolean isFull() {
		return stack.length <= poi;
	}
	
	/**
	 * to add value in side the stack
	 * @return value and increase current position by 1
	 * @exception throw overflow exception
	 * @param pass Object arg0
	 */
	public void push(Object arg0) throws Overflow {
		if(!isFull()){stack[poi++] = arg0;}
		else throw new Overflow("is full");
	}
	
	/**
	 * to see current value
	 * @return current position value
	 * @exception throw Underflow exception
	 */
	public Object examine() throws Underflow {
		if(!isEmpty()) {return stack[poi-1];}
		else throw new Underflow("is empty");
	}
	
	/**
	 * to delete a value in the stack
	 * @exception throw Underflow exception
	 * @return value after pop
	 */
	public Object pop() throws Underflow {
		
		if(!isEmpty()) return (stack[--poi]);
		else throw new Underflow("is empty");
		
	}

}