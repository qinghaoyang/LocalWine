import React from 'react';
import Modal from 'react-modal';
import AddReview from './AddReview';

function WineReviews({ modal, setModal }) {
  if (!modal.isOpen) {
    return null;
  }
  const reviews = modal.wine.reviews;
  console.log('reviews: ', modal.wine);
  return (
    <Modal
      isOpen={modal.isOpen}
      contentLabel="My dialog"
    >
      <div className="flex flex-wrap h-full">
        <div className="flex w-48 h-48">
          <img
            className="rounded"
            src={modal.wine.photo_url}
            alt={modal.wine.name}
          />
        </div>
        <div className="h-48 px-6 py-4">
          <h4
            className="font-bold text-gray-700 text-xl mb-2"
            style={{ fontFamily: "coustard" }}>
            Vineyard: {modal.wine.name}
          </h4>
          <p
            className="text-gray-600 text-base"
            style={{ fontFamily: 'Gentium Basic' }}>
            Variety: {modal.wine.variety}
          </p>
          <p
            className="text-gray-500 text-base"
            style={{ fontFamily: 'Gentium Basic' }}>
            Winery: {
              modal.wine.winery.name + ', '
              + modal.wine.winery.region + ', ' + modal.wine.winery.state
            }
          </p>
        </div>
        <h4 className="font-bold text-gray-700 px-6 text-xl w-full">Reviews</h4>
        <div className="h-1/2 overflow-auto">
          {reviews.map(review => (
            <div className="px-6 py-4 w-full">
              {/* <h4>{review.title}</h4> */}
              <p>{review.taster}</p>
              {review.taster_media ? (
                <a
                  className="italic underline"
                  href={"https://twitter.com/" + review.taster_media.slice(1)}>
                  {review.taster_media}
                </a>
              ) : null}
              <p>{review.rating}/100</p>
              <p>{review.text}</p>
            </div>
          ))}
        </div>
        <AddReview modal={modal} setModal={setModal} />
      </div>
    </Modal>
  )
}

export default WineReviews;