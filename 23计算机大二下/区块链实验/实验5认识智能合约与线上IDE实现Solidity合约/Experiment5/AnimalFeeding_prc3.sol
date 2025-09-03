pragma solidity ^0.4.19;

import "./AnimalIncubators_prc3.sol";

contract AnimalFeeding_prc3 is AnimalIncubators_prc3 {
    function feedAndGrow(uint _animalId, uint _targetDna) internal {
        require(msg.sender == animalToOwner[_animalId]);
        Animal storage myAnimal = animals[_animalId];
        
        require(_isReady(myAnimal));
        
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
    
    function _triggerCooldown(Animal storage _animal) internal {
        _animal.readyTime = uint32(now + cooldownTime);
    }
    
    function _isReady(Animal storage _animal) internal view returns (bool){
        return (_animal.readyTime <= now);
    }
    
}




