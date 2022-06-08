public class WageCalculator{
    public double wagescalculator(int standardhours, int holidayhours, int hourlywage){
        double wage = 0;
        if(standardhours <= 40)
            wage = standardhours * hourlywage;

        if(standardhours>40)
           wage = (hourlywage*40) + ((standardhours-40)*(1.5*hourlywage));

        wage = wage +(2*hourlywage*holidayhours);
        return wage;
    }

}
