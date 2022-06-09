import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.*;

class WageCalculatorTest {

    @Test
    void wage_person() {
        double result = new WageCalculator().wage_person(40,0,20);
        assertEquals(800,result);
    }

    @ParameterizedTest
    @CsvSource({"40,0,20,800","45,0,20,950","48,8,20,1360"})
    void wage_person_test2(int hours,int holiday,int HourlyWage,int result){
        assertEquals(result,new WageCalculator().wage_person(hours,holiday,HourlyWage));
    }


}