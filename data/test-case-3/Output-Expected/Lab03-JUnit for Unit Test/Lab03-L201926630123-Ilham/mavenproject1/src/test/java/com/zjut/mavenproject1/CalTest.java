import org.junit.Test;
import static org.junit.Assert.assertEquals;
 
public class CalTest {
    @Test
    public void testAdd() {
        Cal cal = new Cal();
        int sum = cal.add(1, 2);
        assertEquals(3, sum);
        
        if(sum != 3)
            throw new Exception("Cal.add() has error result for input 1 and 2");
    
        assertEquals(4, cal.add(2, 2));
    }
}
