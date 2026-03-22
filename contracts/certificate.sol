pragma solidity ^0.8.0;

contract CertificateStorage {

    struct Certificate {
        string cert_id;
        string email;
        string name;
        string course;
        string hash;
    }

    mapping(string => Certificate) public certificates;

    function addCertificate(
        string memory cert_id,
        string memory email,
        string memory name,
        string memory course,
        string memory hash
    ) public {
        certificates[cert_id] = Certificate(cert_id, email, name, course, hash);
    }

    function getCertificate(string memory cert_id) public view returns (
        string memory, string memory, string memory, string memory, string memory
    ) {
        Certificate memory c = certificates[cert_id];
        return (c.cert_id, c.email, c.name, c.course, c.hash);
    }
}