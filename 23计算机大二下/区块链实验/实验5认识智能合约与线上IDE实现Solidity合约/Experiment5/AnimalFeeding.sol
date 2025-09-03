pragma solidity ^0.4.19;
import "./AnimalIncubators_prc2.sol";

contract AnimalFeeding is AnimalIncubators_prc2 {
    function feedAndGrow(uint _animalId, uint _targetDna) public {
        require(msg.sender == animalToOwner[_animalId]);
        Animal storage myAnimal = animals[_animalId];
        _targetDna = _targetDna % dnaLength;
        uint newDna = (myAnimal.dna + _targetDna) / 2;
        newDna = newDna - newDna % 100 + 99;
        _createAnimal("No-one", newDna);
    }
    
    function _catchFood(string _name) internal pure returns (uint) {
        uint rand = uint(keccak256(_name));
        return rand;
    }
    
    function feedOnFood(uint _animalId,string _foodId)public{
        uint foodDna=_catchFood(_foodId);
        feedAndGrow(_animalId,foodDna);
    } 
    
}
