import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import BarcodeScannerScreen from './src/screens/BarcodeScanner/BarcodeScannerScreen';
import BasketRecommendationScreen from './src/screens/BasketRecommendation/BasketRecommendationScreen';
import CurrentBasketScreen from './src/screens/CurrentBasket/CurrentBasketScreen';
import ProductAnalysisScreen from './src/screens/ProductAnalysis/ProductAnalysisScreen';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="CurrentBasket">
        <Stack.Screen name="CurrentBasket" component={CurrentBasketScreen} />
        <Stack.Screen name="BarcodeScanner" component={BarcodeScannerScreen} />
        <Stack.Screen name="ProductAnalysis" component={ProductAnalysisScreen} />
        <Stack.Screen name="BasketRecommendation" component={BasketRecommendationScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}


