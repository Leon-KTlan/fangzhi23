pragma solidity ^0.4.19;
import "./AnimalFeeding_prc3.sol";

contract AnimalHelper is AnimalFeeding_prc3 {
    
    modifier aboveLevel(uint _level, uint _animalId) {
        require(animals[_animalId].level >= _level);
        _;
    }
    
    function changeName(uint _animalId, string _newName) external
        aboveLevel(2, _animalId) {
        require(msg.sender == animalToOwner[_animalId]);
        animals[_animalId].name = _newName;
    }
  

    function changeDna(uint _animalId, uint _newDna) external aboveLevel(20, 
        _animalId) {

        require(msg.sender == animalToOwner[_animalId]);
        animals[_animalId].dna = _newDna;
    }
  
    function getAnimalsByOwner(address _owner) external view returns(uint[]) {
        uint[] memory result = new uint[](ownerAnimalCount[_owner]);
        uint counter = 0;
        for (uint i = 0; i < animals.length; i++) {
          if (animalToOwner[i] == _owner) {
            result[counter] = i;
            counter++;
            } 
        }
        return result;
    }
}


