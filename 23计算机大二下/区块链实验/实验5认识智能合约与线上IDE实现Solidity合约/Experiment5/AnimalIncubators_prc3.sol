pragma solidity ^0.4.19;

import "./ownable.sol";

contract AnimalIncubators_prc3 is Ownable {
    uint dnaDigits = 16;
    uint dnaLength = 10 ** dnaDigits;
    uint cooldownTime = 10 seconds;
    
    event NewAnimal(uint animalId, string name, uint dna);
    
    struct Animal {
        string name;
        uint dna; 
        uint32 level;
        uint32 readyTime;
    }
    
    Animal[] public animals;
    
    mapping (uint => address) public animalToOwner;
    mapping (address => uint) ownerAnimalCount;
    
    function _createAnimal(string _name, uint _dna) internal {
        uint id = animals.push(Animal(_name, _dna, 1, uint32(now + cooldownTime))) - 1;
        animalToOwner[id] = msg.sender;
        ownerAnimalCount[msg.sender]++;
        NewAnimal(id, _name, _dna);
    }
    
    function _generateRandomDna(string _str) private view returns (uint) {
        uint rand = uint(keccak256(_str));
        return rand % dnaLength;
    }
    
    function createRandomAnimal(string _name) public {
        require(ownerAnimalCount[msg.sender] == 0);
        uint randDna = _generateRandomDna(_name);
        _createAnimal(_name, randDna);
    } 
    
}
