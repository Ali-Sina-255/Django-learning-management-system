/**
 * @license Copyright (c) 2003-2024, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see LICENSE.md or https://ckeditor.com/legal/ckeditor-oss-license
 */
/**
 * @module utils/dom/getrangefrommouseevent
 */
/**
 * Returns a DOM range from a given point specified by a mouse event.
 *
 * @param domEvent The mouse event.
 * @returns The DOM range.
 */
export default function getRangeFromMouseEvent(domEvent: MouseEvent & {
    rangeParent?: HTMLElement;
    rangeOffset?: number;
}): Range | null;
